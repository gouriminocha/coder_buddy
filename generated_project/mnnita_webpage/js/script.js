// Smooth scrolling helper
function smoothScroll(targetId){
  var el=document.querySelector(targetId);
  if(el){
    window.scrollTo({top:el.offsetTop,behavior:'smooth'});
  }
}

// Navigation link click handling
document.querySelectorAll('nav a').forEach(function(link){
  link.addEventListener('click',function(e){
    e.preventDefault();
    smoothScroll(link.getAttribute('href'));
  });
});

// Optional scroll‑spy to highlight active nav link
window.addEventListener('scroll',function(){
  var sections=document.querySelectorAll('section[id]');
  var current='';
  sections.forEach(function(sec){
    if(window.pageYOffset>=sec.offsetTop-10){
      current=sec.id;
    }
  });
  document.querySelectorAll('nav a').forEach(function(link){
    var isActive=link.getAttribute('href')===('#'+current);
    if(isActive){
      link.classList.add('active');
    }else{
      link.classList.remove('active');
    }
  });
});

// Placeholder form validation
function validateContactForm(event){
  event.preventDefault();
  var form=event.target;
  var name=form.querySelector('[name=name]').value.trim();
  var email=form.querySelector('[name=email]').value.trim();
  var message=form.querySelector('[name=message]').value.trim();
  if(!name||!email||!message){
    alert('Please fill all fields');
    return;
  }
  alert('Form submitted (placeholder)');
}

var contactForm=document.getElementById('contactForm');
if(contactForm){
  contactForm.addEventListener('submit',validateContactForm);
}
