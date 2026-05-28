from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'html/home.html')

def generate_form(request):
    if request.method == "POST":
        name = request.POST.get("name")
        standard = request.POST.get("standard")
        num_subjects = int(request.POST.get("num_subjects"))

        subjects = range(1, num_subjects + 1)

        context = {
            "name": name,
            "standard": standard,
            "subjects": subjects
        }

        return render(request, "html/marks_form.html", context)

    return render(request, "html/home.html")

def result_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        standard = request.POST.get("standard")
        num_subjects = int(request.POST.get("num_subjects"))

        marks = []
        total = 0

        for i in range(1, num_subjects + 1):
            m = int(request.POST.get(f"m{i}"))
            marks.append(m)
            total += m

        percentage = round(total / num_subjects, 2)

        # Logic
        if percentage >= 75:
            grade = "A"
            status = "Pass"
        elif percentage >= 60:
            grade = "B"
            status = "Pass"
        elif percentage >= 50:
            grade = "C"
            status = "Pass"
        else:
            grade = "F"
            status = "Fail"

        context = {
            "name": name,
            "standard": standard,
            "marks": marks,
            "total": total,
            "percentage": percentage,
            "grade": grade,
            "status": status
        }

        return render(request, "html/result.html", context)

    return render(request, "html/home.html")
