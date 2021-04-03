// Obtain all the weather data through the backend API
var get_weather_for_all_cities = async () => {
    var response = await fetch("/api/weathers");
    var content = await response.json();

    return content;
}

// Update raw data table
var update_weather_table = async () => {
    var weather_data = await get_weather_for_all_cities();

    var table = d3.select("tbody");

    //Clear table before rendering
    table.html("");

    weather_data.forEach((d) => {
        var row = table.append("tr")
        row.append("td").text(d["city_name"]);
        row.append("td").text(d["temp"]);
        row.append("td").text(d["feels_like"]);
        row.append("td").text(d["temp_min"]);
        row.append("td").text(d["temp_max"]);
        row.append("td").text(d["pressure"]);
        row.append("td").text(d["humidity"]);
        row.append("td").text(d["wind_speed"]);
        row.append("td").text(d["sunrise"]);
        row.append("td").text(d["sunset"]);
    });
}

update_weather_table();