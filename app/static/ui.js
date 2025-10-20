function scrollToSection(index) {
    const container = document.querySelector('.scroll-wrapper');
    const sectionWidth = container.offsetWidth;
    container.scrollTo({
        left: sectionWidth * index,
        behavior: 'smooth'
    });
}
