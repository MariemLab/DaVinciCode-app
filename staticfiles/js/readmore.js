function toggleReadMore() {
   var paragraphs = document.querySelectorAll('.full-text');
   paragraphs.forEach(function (paragraph) {
      paragraph.classList.toggle('hidden');
   });

   var readMoreLink = document.querySelector('.read_more');
   if (paragraphs[0].classList.contains('hidden')) {
      readMoreLink.textContent = 'READ MORE';
   } else {
      readMoreLink.textContent = 'Réduire';
   }
}
