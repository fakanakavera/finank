from django.shortcuts import render

# make a view that returns a test page DO NOT USE HTML FILE, MAKE THE HTML IN THE VIEW
def test(request):
    return render(request, 'test.html', {})
