# import cv2
# import numpy as np
# import tensorflow as tf
# from rest_framework import generics, status
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from .models import Property, PropertyImages
# from .serializers import PropertyImagesSerializer
# from .permissions import IsOwnerOfProperty
# from django.core.files.base import ContentFile
# from io import BytesIO
# from PIL import Image
# from cloudinary.uploader import upload as cloudinary_upload
# import os
# from django.conf import settings

# def pixel_mse_loss(x, y):
#     return tf.reduce_mean((x - y) ** 2)

# # Load the SRCNN model
# SRCNN = tf.keras.models.load_model(os.path.join(settings.BASE_DIR, "srcnn_model.h5"),custom_objects = {"pixel_mse_loss":pixel_mse_loss})

# class PropertyImagesCreateAPIView(generics.CreateAPIView):
#     permission_classes = (IsAuthenticated, IsOwnerOfProperty)
#     serializer_class = PropertyImagesSerializer
#     queryset = PropertyImages.objects.all()

#     def preprocess_image(self, image):
#         # Read image
#         image = cv2.imdecode(np.frombuffer(image.read(), np.uint8), cv2.IMREAD_COLOR)
#         # Resize image to 256x256
#         image = cv2.resize(image, (256, 256))
#         # Convert to YCrCb color space
#         image_ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
#         # Extract Y channel
#         y_channel = image_ycrcb[:, :, 0].astype(np.float32) / 255.0
#         y_channel = np.expand_dims(y_channel, axis=0)
#         y_channel = np.expand_dims(y_channel, axis=-1)
#         # Expand Y channel to 3 channels (replicating for compatibility)
#         y_channel_rgb = np.repeat(y_channel, 3, axis=-1)
#         return y_channel_rgb, image_ycrcb

#     def optimize_image(self, y_channel_rgb):
#         # Predict high-resolution Y channel
#         optimized_y = SRCNN.predict(y_channel_rgb)
#         # Convert optimized output to a single channel
#         return optimized_y[0, :, :, 0] * 255.0


#     def postprocess_image(self, optimized_y, image_ycrcb):
#         # Replace Y channel with optimized Y
#         image_ycrcb[:, :, 0] = optimized_y.astype(np.uint8)
#         # Convert back to BGR color space
#         optimized_image = cv2.cvtColor(image_ycrcb, cv2.COLOR_YCrCb2BGR)
#         return optimized_image

#     def create(self, request, *args, **kwargs):
#         property_id = request.data.get('property_id')
#         try:
#             property_instance = Property.objects.get(id=property_id)
#         except Property.DoesNotExist:
#             return Response(
#                 {"error": "Property not found."},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         images = request.FILES.getlist('image')

#         if not images:
#             return Response(
#                 {"error": "No images provided."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         image_instances = []
#         for image in images:
#             # Preprocess image
#             y_channel, image_ycrcb = self.preprocess_image(image)
#             # Optimize image
#             optimized_y = self.optimize_image(y_channel)
#             # Postprocess image
#             optimized_image = self.postprocess_image(optimized_y, image_ycrcb)
#             # Save optimized image to Cloudinary
#             optimized_image_pil = Image.fromarray(optimized_image)
#             buffer = BytesIO()
#             optimized_image_pil.save(buffer, format='JPEG')
#             optimized_image_file = ContentFile(buffer.getvalue())
#             cloudinary_response = cloudinary_upload(optimized_image_file)
#             # Create PropertyImages instance
#             image_instance = PropertyImages(property=property_instance, image=cloudinary_response['url'])
#             image_instances.append(image_instance)

#         PropertyImages.objects.bulk_create(image_instances)

#         serializer = self.get_serializer(image_instances, many=True)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

