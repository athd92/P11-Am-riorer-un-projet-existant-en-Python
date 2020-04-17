from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
from .forms import UserFormWithEmail
from .models import Aliment, Favorite
from .form_aliment import FormAliment
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string, get_template

def homepage(request):
    """
    This function returns the homepage template
    """
    return render(request=request, template_name="main/homepage.html")


def register(request):
    """
    This function returns the register form template
    """
    if request.method == "POST":
        form = UserFormWithEmail(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Bienvenue {username}, votre profile est créé!")
            login(request, user)

            return redirect("main:homepage")
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

            return render(
                request=request,
                template_name="main/register.html",
                context={"form": form},
            )

    form = UserFormWithEmail
    return render(
        request=request, template_name="main/register.html", context={"form": form}
    )


def logout_request(request):
    """
    This function is used by the user to logout
    """
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, f"Déconnecté")
        return redirect("main:homepage")
    else:
        return redirect("main:homepage")


def login_request(request):
    """
    This functions is used to get the user logged if
    the Auth is auth is success
    """
    if request.user.is_authenticated:
        return redirect("/")
    else:

        if request.method == "POST":
            form = AuthenticationForm(request=request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password")
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, f"Bienvenue {user.username}")
                    return redirect("/")
                else:
                    pass
            else:
                pass
        form = AuthenticationForm()
        return render(
            request=request, template_name="main/login.html", context={"form": form}
        )


def aliments(request):
    """
    This function returns the results of the initial search
    """
    user = request.user
    aliments_saved = Favorite.objects.filter(saved_by=user.id)
    count = len(aliments_saved)
    flist = []
    for i in aliments_saved:
        flist.append(i.saved_aliment.id)

    fav_aliments = Aliment.objects.filter(pk__in=flist)
    aliments = Favorite.objects.filter(saved_by=user.id)
    count = len(aliments)
    flist = []
    for i in aliments:
        flist.append(i.saved_aliment.id)

    favorites = Aliment.objects.filter(pk__in=flist)
    count_saved = len(favorites)
    aliment_list = Aliment.objects.all()
    query = request.GET.get("aliments")
    if query:
        query = query.capitalize()
        aliment_list = (
            Aliment.objects.filter(name__startswith=query,)
            .exclude(nutriscore="non disponible",)
            .exclude(brands="non disponible")
        )

        aliment_count = aliment_list.count()

        complete_list = zip(fav_aliments, aliment_list)

        paginator = Paginator(aliment_list, 6)  # 6 posts per page
        page = request.GET.get("page")

        try:
            aliments = paginator.page(page)
        except PageNotAnInteger:
            aliments = paginator.page(1)
        except EmptyPage:
            aliments = paginator.page(paginator.num_pages)
        print(fav_aliments)
        context = {
            "fav_aliments": fav_aliments,
            "aliments": aliments,
            "count": aliment_count,
            "query": query,
            "counted_saved": count_saved,
        }
        return render(request, "main/aliments.html", context)
    else:
        return redirect("/")


def account(request):
    """
    This function return the account html templates with the users
    informations
    """
    user = request.user
    aliments = Favorite.objects.filter(saved_by=user.id)

    flist = []
    for i in aliments:
        flist.append(i.saved_aliment.id)

    aliments_list = Aliment.objects.filter(pk__in=flist)
    total = aliments_list.count()
    context = {"total": total}
    if request.user.is_authenticated:
        return render(request, "main/account.html", context)
    else:
        return redirect("/")


def infos(request, aliment_id):
    """
    This function returns an html template with infos about the
    selected aliment
    """
    aliment = Aliment.objects.get(id=aliment_id)
    # name = aliment.name
    date = aliment.date
    date = date[2:12]
    print(f"DATE {date}")
    context = {"aliment": aliment, "date": date, "aliment_id": aliment_id}

    return render(request, "main/infos.html", context)


def save_aliment(request, aliment_id):
    """
    This view adds the selected aliment to the database
    """
    path = request.META.get("HTTP_REFERER")
    aliment = Aliment.objects.get(id=aliment_id)
    saved_aliment = Favorite(saved_by=request.user, saved_aliment=aliment)
    saved_aliment.save()
    saved = Favorite.objects.count()
    query = aliment.name
    query = query.split(" ")
    query = query[0]

    if query:
        aliment_list = (
            Aliment.objects.filter(name__startswith=query,)
            .exclude(nutriscore="non disponible",)
            .exclude(brands="non disponible")
        )
        aliment_count = aliment_list.count()

    paginator = Paginator(aliment_list, 6)  # 6 posts per page
    page = request.GET.get("page")

    try:
        aliments = paginator.page(page)
    except PageNotAnInteger:
        aliments = paginator.page(1)
    except EmptyPage:
        aliments = paginator.page(paginator.num_pages)
    messages.success(request, f"Aliment sauvegardé!")

    return redirect(path)


def alternative(request, aliment_id):
    """
    This view renders an html template with alternative products
    """
    path = request.META.get("HTTP_REFERER")

    try:
        aliment = Aliment.objects.get(id=aliment_id)
    except Aliment.DoesNotExist:
        return redirect("/homepage/")

    categorie = aliment.categories
    categorie_list = categorie.split(" ")
    cat_for_query = categorie_list[0]
    aliment_list = Aliment.objects.filter(
        categories__startswith=cat_for_query, nutriscore="a"
    )
    total = len(aliment_list)

    if total == 0:
        aliment_list = Aliment.objects.filter(
            categories__startswith=cat_for_query, nutriscore="b"
        )
        total = len(aliment_list)
        if total == 0:
            aliment_list = Aliment.objects.filter(
                categories__startswith=cat_for_query, nutriscore="c"
            )
            total = len(aliment_list)
        if total == 0:
            aliment_list = Aliment.objects.filter(
                categories__startswith=cat_for_query, nutriscore="d"
            )
            total = len(aliment_list)

    paginator = Paginator(aliment_list, 6)  # 6 posts per page
    page = request.GET.get("page")

    try:
        aliments = paginator.page(page)
    except PageNotAnInteger:
        aliments = paginator.page(1)
    except EmptyPage:
        aliments = paginator.page(paginator.num_pages)

    context = {"aliments": aliments, "total": total}

    return render(request, "main/alternative.html", context)


def delete(request, aliment_id):
    """This view is used to delete a saved aliment"""

    if request.user.is_authenticated:
        user = request.user
        aliment = Aliment.objects.filter(id=aliment_id)
        favorite_aliment = Favorite.objects.filter(
            saved_aliment__in=aliment, saved_by=user.id
        )
        favorite_aliment.delete()
        return redirect("/saved")
    else:
        return redirect("/saved")


def saved(request):
    """This view is used to a save an aliment"""

    user = request.user
    aliments = Favorite.objects.filter(saved_by=user.id)
    count = len(aliments)
    flist = []
    for i in aliments:
        flist.append(i.saved_aliment.id)

    aliments_list = Aliment.objects.filter(pk__in=flist)
    paginator = Paginator(aliments_list, 6)  # Show 25 contacts per page

    page = request.GET.get("page")
    aliments = paginator.get_page(page)

    context = {
        "aliments": aliments,
        "count": count,
    }
    if user.is_authenticated:
        return render(request, "main/saved.html", context)
    else:
        return redirect("main:login")


def mentions(request):
    """This view is used to display the mentions page"""

    return render(request, "main/mentions.html")


def delete_from_main(request, aliment_id):
    """
    This view is used to delete a saved aliment
    from the main aliment page
    """
    path = request.META.get("HTTP_REFERER")

    if request.user.is_authenticated:
        user = request.user
        aliment = Aliment.objects.filter(id=aliment_id)
        favorite_aliment = Favorite.objects.filter(
            saved_aliment__in=aliment, saved_by=user.id
        )
        favorite_aliment.delete()
        return redirect(path)
    else:
        return redirect(path)


def send_infos(request, aliment_id):
    """
    Function used to send aliment infos by mail
    """
    path = request.META.get("HTTP_REFERER")
    if request.user.is_authenticated:
        email = request.user.email
        email_from = settings.EMAIL_HOST_USER

        subject = 'Fiche aliment'
        message = 'Voici la fiche demandée'


        subject, from_email, to = 'Fiche aliment Purbeurre', email_from, email_from
        text_content = 'Une petite faim? Voici les informations demandées.'
        context = {'test':"test"}
        html_content = render_to_string('main/email_notif.html', context)


        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    







        print("ALIMENT ID ")
        print(aliment_id)
        aliment = Aliment.objects.filter(id=aliment_id)
        for i in aliment:
            print(i.ingredients_fr)
        messages.success(request, f"Message envoyé sur votre messagerie!")

        return redirect(path)
