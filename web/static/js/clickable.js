$('a.clickable').click(function() {
  $.get(this.href);
  $icon = $(this).children("img")[0]
  $($icon).toggleClass("on");
  return false;
});
