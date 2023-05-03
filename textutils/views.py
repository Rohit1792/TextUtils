from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, "index.html")


def analyze(request):
    djtext = request.POST.get("text", "default")

    userCount = request.POST.get("usercount", "default")
    user = request.POST.get("user", "default")
    removepunc = request.POST.get("removepunc", "off")
    fullcaps = request.POST.get("fullcaps", "off")
    capfirst = request.POST.get("capfirst", "off")
    newline = request.POST.get("newline", "off")
    extraspaceremover = request.POST.get("extraspaceremover", "off")
    charcount = request.POST.get("charcount", "off")

    purpose = ""
    if removepunc == "on":
        punc = """!()-[]{};:'"\,<>./?@#$%^&*_~"""
        analyze = ""
        for char in djtext:
            if char not in punc:
                analyze = analyze + char
        purpose += "Removed Punctuation"
        djtext = analyze

    if fullcaps == "on":
        analyze = ""
        for char in djtext:
            analyze = analyze + char.upper()

        purpose += ", Changed to Uppercase"
        djtext = analyze

    if capfirst == "on":
        analyze = djtext.capitalize()

        purpose += ", Capitalized First Letter"
        djtext = analyze

    if newline == "on":
        analyze = ""
        # for char in djtext:
        # if char != "\n" and char != "\r":

        # analyze = analyze + char
        analyze = analyze + djtext.replace("\r\n", " ")
        purpose += ", Removed New line"
        djtext = analyze

    if extraspaceremover == "on":
        analyze = ""
        for index, char in enumerate(djtext):
            if not (djtext[index] == " " and djtext[index+1] == " "):
                analyze = analyze + char
        # analyze = analyze + djtext.replace("  ", " ")

        purpose += ", Extra Spaces Removed"
        djtext = analyze

    if charcount == "on":
        if user == "on" and userCount != "":
            for char in userCount:
                countChar = djtext.count(char)
        else:
            charLen = len(djtext)
            countS = djtext.count(" ")
            countChar = charLen - countS

        count = f"The number of character in the text is: {countChar}"
        purpose += ", Character Counted"
        djtext = analyze
    if (removepunc != "on" and fullcaps != "on" and capfirst != "on" and newline != "on" and extraspaceremover != "on" and charcount != "on"):
        return HttpResponse("<h1>Error</h1>")

    # else:
    #     return HttpResponse("<h1>Error!</h1>")

    if charcount == "on":
        params = {"purpose": f"{purpose}",
                  "analyzed_text": f"{analyze}", "counter": f"{count}"}
    else:
        params = {"purpose": f"{purpose}", "analyzed_text": f"{analyze}"}
    return render(request, "analyze.html", params)

# removepunc=on&fullcaps=on&capfirst=on&newline=on&extraspaceremover=on
