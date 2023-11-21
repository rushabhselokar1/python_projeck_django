from django.shortcuts import render
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SignUpForm
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from .forms import UploadFileForm
from .models import UploadedFile
from django.http import JsonResponse
from PIL import Image, ImageOps
import tensorflow as tf
import os
import numpy as np
from web_application.utils.list_of_fields_question import fields_questions_list_for_invoice,fields_questions_list_for_bills
from web_application.utils.text_getter import generate_result

# this view is for home page
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,(f"Welcome {username}. You have been Logged in Successfully.!"))
            return redirect('home')
        else:
            messages.error(request,("There was an error logining in. Please try again.!"))
            return redirect('login')        
    else: 
        return render(request, 'login.html',{})

def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # log in user
            user = authenticate(username=username,password=password)
            login(request,user)
            messages.success(request,("You have been Registered Successfully.! Login to your account..."))
            return redirect('login')
        else:
            messages.success(request,("There was an error in registering. Please try again.!"))
            return redirect('register')
    else:
        return render(request, 'register.html',{'form':form})

def logout_user(request):
    logout(request)
    messages.success(request,("You have been logged out."))
    return redirect('home')
 
def upload_invoice(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,("Image uploaded successfully."))
            return redirect('show_files')
    else:
           # messages.success(request,("Upload failed. Try again."))
            form = UploadFileForm()
    return render(request,'upload_invoice.html', {'form': form})      

def show_files(request):
    files = UploadedFile.objects.order_by('-file_id')
    return render(request, 'show_files.html', {'files': files})
    
def classification_prediction(request):
    if request.method=='POST':
        # img_file contains path to the image file in media which is in string
        img_file = request.POST['imgFile']
        file_id = request.POST['file_id']
        print('File Id: ',file_id)
  
        # loading the model from model directory
        model = tf.keras.models.load_model("models/keras_Model.h5", compile=False)
        
        # Load the image classification labels
        with open("models/labels.txt", "r") as labels_file:
            class_names = [line.strip() for line in labels_file.readlines()]
        
        # openin the image from the img_file path with pillow Image
        image_classify = Image.open('.'+ img_file).convert("RGB")
        
        # setting the size of the image as desired for the model
        img_size = (224, 224)
        # resize and crop an image to fit within a specified bounding box while maintaining its aspect ratio. 
        # It takes three arguments: 
        # the image to be resized (image_classify), 
        # #the target size (img_size),
        # and the resampling filter to be used.
        image_classify = ImageOps.fit(image_classify, img_size, Image.Resampling.LANCZOS)
        # convert image to array
        image_array_classify = np.asarray(image_classify)
        # normalize the image array
        normalized_image_array_classify = (image_array_classify.astype(np.float32) / 127.5) - 1
        '''
        So, the code below is creating a four-dimensional NumPy array to hold image data for classification, 
        where each image has dimensions of 224x224 pixels with three color channels (RGB). 
        The normalized pixel values of the image are then assigned to the first element of this array. 
        This array is  used as input data for machine learning models.
        '''
        data_classify = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        data_classify[0] = normalized_image_array_classify
        
        # Make a prediction for image classification
        prediction_classify = model.predict(data_classify)
        index_classify = np.argmax(prediction_classify)
        class_name_classify = class_names[index_classify]
        confidence_score_classify = prediction_classify[0][index_classify]
        confidence_score_classify = confidence_score_classify*100

        
        # Display the classification prediction and confidence score
        value=f"{class_name_classify[2:]}"
        
        #global class_name
        class_name = f"{class_name_classify[2:]}"
        confidence_score =f"{confidence_score_classify:.2f} %"
        messages.success(request,("Image Classification Completed Successfully."))

    return render(request, 'classification_prediction.html',{'img_file':img_file,'file_id':file_id,'class_name':class_name,'confidence_score':confidence_score})

def text_extraction_page(request):    
    if request.method=='POST':
        # class_name is the invoice classfied type
        class_name = request.POST['class_name']
        print("Class Name : ",class_name)
        # img_file contains path to the image file in media which is in string
        img_file = request.POST['img_file']
        print("Image Path: ",img_file)
        image = Image.open('.'+ img_file).convert("RGB")
    
    return render(request,'text_extraction_page.html',{'class_name':class_name,
        'img_file':img_file,
        'fields_questions_list_for_invoice':fields_questions_list_for_invoice,
        'fields_questions_list_for_bills':fields_questions_list_for_bills})

def text_show_files(request):
    if request.method =="POST":
        img_file = request.POST['img_file']
        class_name = request.POST['class_name']
        image = Image.open('.'+ img_file).convert("RGB")    
            
        # getting the selected fields from checkbox.
        selected_fields = request.POST.getlist('selected_fields')
        print("Selected Fields:", selected_fields)
        
        selected_questions = []
        if class_name == "Invoices":
            # getting the selected questions for the respective fields
            for field in selected_fields:
                #print(fields_questions_list_for_invoice[field])
                selected_question = fields_questions_list_for_invoice[field]
                selected_questions.append(selected_question)
            print("Selected Questions:",selected_questions)
        elif class_name == "Restaurant_Bill":
            for field in selected_fields:
                #print(fields_questions_list_for_invoice[field])
                selected_question = fields_questions_list_for_bills[field]
                selected_questions.append(selected_question)
            print("Selected Questions:",selected_questions)
        else:
            return HttpResponse("Under Process")
            
        selected_dict = dict(zip(selected_fields, selected_questions))
        
        print('Selected Dictionary: ',selected_dict)
        
        extracted_data = {}
        
        if class_name == "Invoices":
            for field,question in selected_dict.items():
                user_question = question
                answer = str.upper(generate_result(user_question,image))
                extracted_data[field]=answer
            print("Extracted Data: ",extracted_data)
        elif class_name == 'Restaurant_Bill':
            for field,question in selected_dict.items():
                user_question = question
                answer = str.upper(generate_result(user_question,image))
                extracted_data[field]=answer
            print("Extracted Data: ",extracted_data)
        else:
            pass           
        messages.success(request,("Data Extraction Successfull...!"))
    return render(request, 'text_show_files.html',{'img_file':img_file,'extracted_data':extracted_data}) 

def verify_predictions(request):
    if request.method == 'POST':
        file_id = request.POST.get('file_id')
        class_name = request.POST.get('class_name')
        confidence_score = request.POST.get('confidence_score')
        img_file = request.POST.get('img_file')
        file = UploadedFile.objects.get(pk=file_id)
        print("Class Name: ",class_name)
        print("Confidence Score: ",confidence_score)
    return render(request,'verify_predictions.html', {'file': file,'class_name': class_name,'confidence_score': confidence_score,'img_file':img_file})
