
const doCalculation=()=>{
    fetch('http://localhost:5000/results')
        .then((response) => {
            console.log(response);
            return response.json(); 
        }).then((result) => {
            console.log(result);
            resultsImg.src=result.image
        }).catch((err) => {
            console.log('錯誤:', err);
    });
}
const getTourData = async() =>{
    console.log("start fetching data")
    const data = await fetch('http://localhost:5000/tour')
    const jsonData = await data.json();
    console.log(jsonData)
}

var calculate_button = document.getElementById('calculate-button')
var slider = document.getElementById("myRange");
var threshold = document.getElementById("threshold");
var resultsImg = document.getElementById('results-plot')
threshold.innerHTML = slider.value; // Display the default slider value

// Update the current slider value (each time you drag the slider handle)
slider.oninput = function() {
  threshold.innerHTML = this.value;
}
// calculate_button.addEventListener("click", doCalculation)



calculate_button.addEventListener("click", getTourData)

