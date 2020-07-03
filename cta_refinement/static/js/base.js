//Ajax call to place fisher-mutual-exclusion sample script in editor

$(function() {
  $('#fisher-link').bind('click',function() {
    $.getJSON($SCRIPT_ROOT + '/sample-scripts/fisher-mutual-exclusion', {
    }, function(data) {
      editor.setValue(data.src);
    });
    return false;
  });
});

//Ajax call to place ford-credit-portal sample script in editor

$(function() {
  $('#ford-link').bind('click',function() {
    $.getJSON($SCRIPT_ROOT + '/sample-scripts/ford-credit-portal', {
    }, function(data) {
      editor.setValue(data.src);
    });
    return false;
  });
});

//Ajax call to place ooi-word-counting sample script in editor

$(function() {
  $('#ooi-link').bind('click',function() {
    $.getJSON($SCRIPT_ROOT + '/sample-scripts/ooi-word-counting', {
    }, function(data) {
      editor.setValue(data.src);
    });
    return false;
  });
});

//Ajax call to place scheduled-task-protocol sample script in editor

$(function() {
  $('#sched-link').bind('click',function() {
    $.getJSON($SCRIPT_ROOT + '/sample-scripts/scheduled-task-protocol', {
    }, function(data) {
      editor.setValue(data.src);
    });
    return false;
  });
});

//Ajax call to place smtp-client sample script in editor

$(function() {
  $('#smtp-link').bind('click',function() {
    $.getJSON($SCRIPT_ROOT + '/sample-scripts/smtp-client', {
    }, function(data) {
      editor.setValue(data.src);
    });
    return false;
  });
});

//Ajax call to place atm sample script in editor

$(function() {
 $('#atm-link').bind('click',function() {
   $.getJSON($SCRIPT_ROOT + '/sample-scripts/atm', {
   }, function(data) {
     editor.setValue(data.src);
   });
   return false;
 });
});
