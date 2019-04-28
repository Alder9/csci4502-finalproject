// d3.json("../php/getdata.php", function(error, data){
//     if(error) {
//         console.log(error);
//     }
//     console.log(data);
// })

fetch('./php/getdata.php').then((response) => {
    console.log(response);
    return response.json();
});

// alert("../php/getdata.php");