document.addEventListener('DOMContentLoaded', () => {
    const verticalMenu = document.getElementById('vertical-menu');

    document.addEventListener('touchstart', handleTouchStart, false);
    document.addEventListener('touchmove', handleTouchMove, false);

    let xDown = null;
    let yDown = null;

    function handleTouchStart(evt) {
        const firstTouch = evt.touches[0];
        xDown = firstTouch.clientX;
        yDown = firstTouch.clientY;
    }

    function handleTouchMove(evt) {
        if (!xDown || !yDown) {
            return;
        }

        const xUp = evt.touches[0].clientX;
        const yUp = evt.touches[0].clientY;

        const xDiff = xDown - xUp;
        const yDiff = yDown - yUp;

        if (Math.abs(xDiff) > Math.abs(yDiff)) {
            if (xDiff > 0) {
                verticalMenu.classList.add('show');
            } else {
                verticalMenu.classList.remove('show');
            }
        }
        xDown = null;
        yDown = null;
    }

    function scrollToProduct(productId) {
        const productElement = document.querySelector(`.product[data-product-id="${productId}"]`);
        if (productElement) {
            productElement.scrollIntoView({
                behavior: 'smooth'
            });
        }
    }
});