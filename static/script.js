$(function() {
    $('#generalInfo').click(function(event) {
        $.ajax({
            url: this.form.action,
            data: $('#generalForm').serialize(),
            type: 'POST',
            success: function(response){
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
    $('#scientificAbstract').click(function(event) {
        $.ajax({
            url: this.form.action,
            data: $('#scientificAbstractForm').serialize(),
            type: 'POST',
            success: function(response){
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });

    $('#layAbstract').click(function(event) {
        $.ajax({
            url: this.form.action,
            data: $('#layAbsractForm').serialize(),
            type: 'POST',
            success: function(response){
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });

    $('#submitForm').click(function(event) {
        $.ajax({
            url: this.form.action,
            data: $('Form').serialize(),
            type: 'POST',
            success: function(response){
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });






});