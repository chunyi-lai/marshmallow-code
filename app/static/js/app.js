var get_weather_for_all_cities = async () => {
    var response = await fetch("/api/weathers");
    var content = await response.json();

    return content;
}

var update_weather_info = (info) => {
    var summary = d3.selectAll("#summary");
    summary.html("");
    summary.append("ul")
        .append("li").text("City -- " + info["city_name"])
        .append("li").text("Sunrise -- " + info["sunrise"])
        .append("li").text("Sunset -- " + info["sunset"]);
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

    // Update weather info on each board
    update_weather_info(selected_city_weather);
}

load_weather_info();