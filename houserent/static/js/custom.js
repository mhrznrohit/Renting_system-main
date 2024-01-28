document.addEventListener('DOMContentLoaded', function () {
    const locationSlider = new Slider('#location-slider', {
        tooltip: 'always',
    });

    const locationValue = document.getElementById('location-value');

    // Initial update
    updateLocationValue(locationSlider.getValue());

    // Update on slider input
    locationSlider.on('slide', function (value) {
        updateLocationValue(value);
    });

    function updateLocationValue(value) {
        locationValue.textContent = `${value} km`;
        // You can use 'value' for any further processing or API requests
    }
});
