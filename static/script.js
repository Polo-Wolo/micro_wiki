console.log("script.js loaded");

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.navbar-burger').forEach(burger => {
    burger.addEventListener('click', () => {
      const target = document.getElementById(burger.dataset.target);
      burger.classList.toggle('is-active');
      target.classList.toggle('is-active');
    });
  });
});

document.addEventListener("DOMContentLoaded", () => {
  const headings = document.querySelectorAll(
    "h1[id], h2[id], h3[id]"
  );

  const tocLinks = document.querySelectorAll(".toc-link");

  if (!headings.length || !tocLinks.length) return;

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const id = entry.target.id;

          tocLinks.forEach(link => {
            link.classList.toggle(
              "is-active",
              link.getAttribute("href") === `#${id}`
            );
          });
        }
      });
    },
    {
      rootMargin: "-30% 0px -60% 0px",
      threshold: 0
    }
  );

  headings.forEach(h => observer.observe(h));
});
