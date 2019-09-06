$(".registration-form").submit(function(e){
    // prevent from normal form behaviour
    e.preventDefault();
    $('body, #submit').css('cursor', 'progress');
    // serialize the form data
    var serializedData = $(this).serialize();
    $.ajax({
        type : 'POST',
        url :  '',
        data : serializedData,
        success : function(response){
    //reset the form after successful submit
            $("#name, #major, #email").val('');
            $("#year1, #year2, #year3, #year4").prop('checked', false);
            $('body, #submit').css('cursor', 'default');
        location.href='#popup-10';
        },
        error : function(response){
        alert(response);
        }

    });
    return false;
});