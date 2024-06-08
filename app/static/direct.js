function toggleLight() {
  var lightStatus = $("#lightToggle").is(":checked");
  var data = { 'lightStatus': lightStatus };

  $.ajax({
    url: '/toggle-light',
    type: 'POST',
    contentType: 'application/json',
    data: JSON.stringify(data),
  });
}

function toggleDoor() {
  var doorStatus = $("#doorToggle").is(":checked");
  var data = { 'doorStatus': doorStatus };

  $.ajax({
    url: '/toggle-door',
    type: 'POST',
    contentType: 'application/json',
    data: JSON.stringify(data),
  });
}

function toggleFan() {
  var fanStatus = $("#fanToggle").is(":checked");
  var fanSpeeds = document.getElementById('fanSpeeds');

  var data = { 'fanStatus': fanStatus };
  $.ajax({
    url: '/toggle-fan',
    type: 'POST',
    contentType: 'application/json',
    data: JSON.stringify(data),
  });
  if (fanStatus) {
    fanSpeeds.style.display = "block";
    // alert("Fan toggled on");
  } else {
    fanSpeeds.style.display = "none";
    var radios = document.getElementsByName('fanSpeed');
    for (var i = 0; i < radios.length; i++) {
      radios[i].checked = false;
    }
  }
}

function notifySpeed(speed) {
  // alert("Fan speed set to: " + speed);
  
  var data = { 'fanSpeed': speed };
  $.ajax({
    url: '/toggle-fan',
    type: 'POST',
    contentType: 'application/json',
    data: JSON.stringify(data),
  });
}

function getDeviceStatus() {
    $.ajax({
        type: 'GET',
        url: '/get-device-status',
        success: function(data) {
            updateDeviceStatus(data);
        },
        error: function(xhr, status, error) {
            console.error('Error:', error);
        }
    });
}

function updateDeviceStatus(data) {
    $('#lightStatus').text(data.light);
    $('#fanStatus').text(data.fan);
    $('#doorStatus').text(data.door);
}

getDeviceStatus();

setInterval(function() {
    getDeviceStatus();
}, 100);


