search=document.getElementById("q")



document.addEventListener('DOMContentLoaded', function() {

    document.querySelector('#q').onchange = function() {
        const search = document.querySelector('#q').value;

        fetch("https://api.exchangeratesapi.io/latest?base=USD&access_key=ACCESS_KEY")
        .then(response => response.json())
        .then(data => {
            console.log(data)
            const rate =' data.rates.EUR';
            document.querySelector('body').innerHTML = rate;
        })
        .catch(error => {
            console.log('Error:', error);
        });
    
    };


});