// if the current temp is less than 20 makle the weather box blue
// if greater or equal to 20 then make it red 
temp = document.getElementById('current_tempdisp').innerHTML;
boxcolor = document.getElementById('weatherbox');
separator = document.getElementById('separator');

if (temp >= 20){
    boxcolor.classList.add('weatherboxhot');
    separator.classList.add('separatorhot');
}