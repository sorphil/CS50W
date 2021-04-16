from io import TextIOBase
from django.http.response import Http404
from django.shortcuts import render 
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, "singlepage/index.html")

texts = ["Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas ut dignissim massa. Cras sodales tempor risus sed lacinia. Sed laoreet velit nec dui dapibus placerat. Sed ullamcorper bibendum eros, eu tristique tortor mattis ac. Nullam vehicula lacus eget sem viverra ullamcorper. Integer imperdiet mi faucibus tellus pretium aliquet. Aenean mollis rhoncus nibh, in blandit lacus ultrices ac. Duis pharetra nibh sed nunc placerat, non ultricies magna convallis. Vestibulum ac posuere nisl. Nulla malesuada tellus metus, vel volutpat nunc molestie in. Proin non suscipit nulla, eget aliquet dui. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Phasellus ultricies dignissim purus, sit amet sollicitudin diam bibendum mattis. Suspendisse condimentum velit elementum turpis scelerisque vulputate. In elementum feugiat consequat.",
"In vehicula finibus nibh, ut aliquet augue. Vestibulum finibus pretium quam, eu molestie risus luctus euismod. Nulla facilisi. Vestibulum vel magna ligula. Nam eget consequat leo. Mauris hendrerit, eros vel dapibus dapibus, urna mauris dictum arcu, vel pulvinar quam tellus a arcu. Vivamus auctor vulputate felis, in porttitor quam tempor scelerisque. Sed libero orci, mattis quis varius vitae, dictum rutrum libero. Curabitur et rhoncus nibh, sit amet pulvinar lacus. Vivamus et felis a enim finibus sodales. Etiam imperdiet mauris sit amet pulvinar luctus.",
"In porta, ligula in luctus tempor, turpis odio dignissim felis, porta vestibulum est urna in lectus. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Duis ut nunc in ante sagittis accumsan. Praesent facilisis orci nisi, ultrices eleifend metus varius sed. Maecenas fermentum iaculis velit eu aliquam. Mauris suscipit justo a egestas convallis. Vivamus in iaculis turpis. Praesent quis rhoncus orci, non vehicula dolor."]

def section(request, num):
    if 1 <= num <= 3:
        return HttpResponse(texts[num-1])
    else:
        raise Http404("No such section")