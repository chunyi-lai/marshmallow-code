// Obtain all the weather data through the backend API
var get_weather_for_all_cities = async () => {
    var response = await fetch("/api/weathers");
    var content = await response.json();

    return content;
}

// function for wind speed event change
var wind_speed_unit_changed = async () => {
    var all_info = await get_weather_for_all_cities();
    var selected_city = d3.select("#selCity").node().value;
    var selected_info = all_info.filter(d => d.city_name == selected_city)[0];
    console.log(selected_info);
    var wind = d3.selectAll("#wind");
    wind.html('<div class="spinner-border text-primary" role="status">' + 
        '<span class="sr-only">Loading...</span>' + 
    '</div>');
    update_wind_speed(selected_info);
}

// function to update the wind evet handling
var update_wind_speed = (info) => {
    // Get the speed unit
    var current_speed_unit = d3.selectAll("#speed_unit").node().value;
    var speeds = {
        "m/s": Math.round(info["wind_speed"] * 100) / 100, 
        "km/h": Math.round(3.6 * info["wind_speed"] * 100) / 100, 
        "mph": Math.round(2.25 * info["wind_speed"] * 100) / 100
    };

    // Update the DOM tree element
    var wind = d3.selectAll("#wind");
    wind.html("");
    wind.append("ul")
        .append("li").text("Wind Speed -- " 
            + speeds[current_speed_unit]  + " " + current_speed_unit);
}

// function for tempurature event handling
var tempurature_unit_changed = async () => {
    var all_info = await get_weather_for_all_cities();
    var selected_city = d3.select("#selCity").node().value;
    var selected_info = all_info.filter(d => d.city_name == selected_city)[0];
    var wind = d3.selectAll("tempurature");
    wind.html('<div class="spinner-border text-primary" role="status">' + 
        '<span class="sr-only">Loading...</span>' + 
    '</div>');
    update_tempurature(selected_info);
}

//function to update the tempurature
var update_tempurature = (info) => {
    // Get the tempurature unit
    var current_tempurature_unit = d3.selectAll("#tempurature_unit").node().value;
    var original_temps = [info["temp"], info["temp_min"], info["temp_max"], info["feels_like"]]
    var tempuratures = {
        "Kelvin": original_temps.map(d => Math.round(d * 100) / 100), 
        "Celcius": original_temps.map(d => Math.round((d - 273) * 100) / 100),
        "Fahrenheit": original_temps.map(d => Math.round((d - 273) * 9 / 5 + 32) / 100)
    }
    var tempurature = d3.selectAll("#tempurature");
    tempurature.html("");
    tempurature.append("ul")
        .append("li").text("Tempurature -- " + tempuratures[current_tempurature_unit][0] 
            + " Degrees " + current_tempurature_unit)
        .append("li").text("Maximum Tempurature -- " + tempuratures[current_tempurature_unit][1] 
            + " Degrees " + current_tempurature_unit)
        .append("li").text("Minimum Tempurature -- " + tempuratures[current_tempurature_unit][2] 
            + " Degrees " + current_tempurature_unit)
        .append("li").text("Feels like -- " + tempuratures[current_tempurature_unit][3] 
            + " Degrees " + current_tempurature_unit)
}

var update_sun_light = (info) => {
    var sun_light = d3.selectAll("#sun_light");
    sun_light.html("");
    sun_light.append("ul")
        .append("li").text("Sunrise -- " + info["sunrise"])
        .append("li").text("Sunset -- " + info["sunset"]); 
}

// Update the pressure board
var update_pressure = (info) => {
    var pressure = d3.selectAll("#pressure");
    pressure.html("");
    pressure.append("ul")
        .append("li").text("Pressure -- " + info["pressure"] + " hpa");
}

// Update humidity
var update_humidity = (info) => {
    var humidity = d3.selectAll("#humidity");
    humidity.html("");
    humidity.append("ul")
        .append("li").text("Humidity -- " + info["humidity"] + " %")
}

// Update the weather information for each dashboard
var update_weather_info = (info) => {
    // Update sun light information
    update_sun_light(info);
    
    // Update the wind speed board
    update_wind_speed(info);
    
    // Update the tempurature board
    update_tempurature(info);

    // Update the pressure board
    update_pressure(info);

    // Update the humidity board
    update_humidity(info);
}

var load_weather_info = async () => {

    // Obtain weather data
    var weather_data = await get_weather_for_all_cities();
    
    // Obtain all the cities in sorted order
    var cities = weather_data.map(d => d.city_name).sort();

    // Identify the city drop down
    var dropdownMenu = d3.selectAll("#selCity");

    // Add cities to the city drop down
    cities.forEach(city => {
        dropdownMenu.append("option").attr("value", city).text(city);
    });

    // Obtain the currently selected city
    var selected_city = d3.select("#selCity").node().value;

    // Obtain the weather information for currently selected weather
    var selected_city_weather = weather_data.filter(d => d["city_name"] == selected_city)[0];

    // Update day light information
    update_weather_info(selected_city_weather);
}

var city_changed = async () => {
    //Get new weather data
    var weather_data = await get_weather_for_all_cities();

    // Obtain the currently selected city
    var selected_city = d3.select("#selCity").node().value;

    // Obtain the weather information for currently selected weather
    var selected_city_weather = weather_data.filter(d => d["city_name"] == selected_city)[0];

    // Update day light information
    update_weather_info(selected_city_weather);
}

load_weather_info();