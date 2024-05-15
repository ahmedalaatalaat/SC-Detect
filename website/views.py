from mobile_api.ai_model import utils as ai_utils
from django.shortcuts import render
from mobile_api.models import *


def home(request):
    result = False
    if request.method == "POST":
        # create record in database
        scd_history = SCDHistory.objects.create(
            image=request.FILES.get('image'),
            user=request.user
        )
        # send image path to the AI model to predict the disease
        result = ai_utils.predict_cancer_disease(scd_history.image.path)
        # save the predicated disease in the database
        scd_history.diagnose = result
        scd_history.save()
    
    data = {
        "result": result,
    }
    return render(request, "website/home.html", context = data)