from django.db import models

class UploadedFile(models.Model):
    class InvoiceType(models.TextChoices):
        RESTURANT = 'Resturant_Bill'
        INVOICE = 'Invoice' 
        HOTEL = 'Hotel_Stay_Bill'
        TRAVEL = 'Travel_Bill'
        FUEL = 'Fuel_Bill'

    
    file_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100,choices=InvoiceType.choices,default=InvoiceType.INVOICE)
    file = models.ImageField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
# class ClassificationPredictions(models.Model):
#     class InvoiceType(models.TextChoices):
#         RESTURANT = 'Resturant_Bill'
#         INVOICE = 'Invoice' 
#         HOTEL = 'Hotel_Stay_Bill'
#         TRAVEL = 'Travel_Bill'
#         FUEL = 'Fuel_Bill'
    
#     file_id = models.ForeignKey(UploadedFile,null=False,on_delete=models.CASCADE)
#     title = models.CharField(choices=InvoiceType.choices,)
#     class_name_predicted = models.CharField()
#     confidence_score = models.FloatField()
#     predicted_at = models.DateTimeField(auto_now_add=True)
    

