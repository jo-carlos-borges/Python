function atualizarAnimacao(chances) {
    const boneco = document.querySelector('.boneco');

    if (chances === 0) {
        boneco.classList.add('morto');
    } else if (chances <= 3) {
        boneco.classList.add('correndo');
    } else {
        boneco.classList.remove('correndo', 'morto');
    }
}