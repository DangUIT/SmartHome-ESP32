$(document).ready(function () {
    const temp = {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: "Temperature",
                backgroundColor: 'rgba(255, 69, 0, 0.5)',
                borderColor: 'rgb(255, 69, 0)',
                data: [],
                fill: true,
                lineTension: 0.5
            }],
        },
        options: {
            responsive: true,
            title: {
                display: true,
                text: 'Temperature'
            },
            tooltips: {
                mode: 'index',
                intersect: false,
            },
            hover: {
                mode: 'nearest',
                intersect: true
            },
            scales: {
                xAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Time'
                    }
                }],
                yAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Value'
                    }
                }]
            }
        }
    };

    const humi = {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: "Humidity",
                backgroundColor: 'rgba(0, 191, 255, 0.5)',
                borderColor: 'rgb(0, 191, 255)',
                data: [],
                fill: true,
                lineTension: 0.5
            }],
        },
        options: {
            responsive: true,
            title: {
                display: true,
                text: 'Humidity'
            },
            tooltips: {
                mode: 'index',
                intersect: false,
            },
            hover: {
                mode: 'nearest',
                intersect: true
            },
            scales: {
                xAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Time'
                    }
                }],
                yAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Value'
                    }
                }]
            }
        }
    };

    const tempContext = document.getElementById('tempChart').getContext('2d');

    const humiContext = document.getElementById('humiChart').getContext('2d');

    const tempChart = new Chart(tempContext, temp);

    const humiChart = new Chart(humiContext, humi);

    const source = new EventSource("/grapth");

    source.onmessage = function (event) {
        const data = JSON.parse(event.data);
        document.getElementById('t1').innerText = data.temp_value.toFixed(1);
        document.getElementById('h1').innerText = data.humi_value.toFixed(1);
        if (temp.data.labels.length === 15) {
            temp.data.labels.shift();
            temp.data.datasets[0].data.shift();
        }
        if (humi.data.labels.length === 15) {
            humi.data.labels.shift();
            humi.data.datasets[0].data.shift();
        }
        temp.data.labels.push(data.temp_time);
        temp.data.datasets[0].data.push(data.temp_value);
        humi.data.labels.push(data.humi_time);
        humi.data.datasets[0].data.push(data.humi_value);
        tempChart.update();
        humiChart.update();
    }
});