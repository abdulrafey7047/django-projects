function get_post_data(csrf_token, doctor_id, date){
    let post_data = {
        "csrfmiddlewaretoken": csrf_token,
        'doctor_id': doctor_id,
        'date': date,
    }
    return post_data
}

function update_time_slots(csrf_token, doctor_id, date, available_time_slots_url){

    let post_data = get_post_data(csrf_token, doctor_id, date)
    if (post_data.doctor_id > 0 && post_data.date){
        $.post(available_time_slots_url , post_data, function(response) {
            available_time_slots = response
            updated_options = ''
            for (const available_time_slot in available_time_slots){
                updated_options += '<option ' + 'value=' + available_time_slot + '>' + available_time_slots[available_time_slot] + '</option>\n'
            }
            $("#id_time_slot_id").html(updated_options)
            $("#id_time_slot_id").val()

        });
    }
}

