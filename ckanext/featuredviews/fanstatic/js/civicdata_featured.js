$(document).ready(function(){
    ckanapi = new CKAN.Client(location.protocol + "//" + location.host)

    var active_view = $('li.active.view_item:first').data('id')

    $('#canonical').click(function(){
        data = {
            'resource_view_id': active_view,
            'organizationpage': $('#organizationpage').hasClass('active'),
            'canonical': !$(this).hasClass('active')
        }
        ckanapi.action('civicdata_featured_upsert', data, function(err, result){
            if (err == null){
                if (result['result']['canonical'] === 'True'){
                    $('#canonical').addClass('active');
                } else {
                    $('#canonical').removeClass('active');
                }
            }
        })
    });

    $('#organizationpage').click(function(){
        data = {
            'resource_view_id': active_view,
            'organizationpage': !$(this).hasClass('active'),
            'canonical': $('#canonical').hasClass('active')
        }
        ckanapi.action('civicdata_featured_upsert', data, function(err, result){
            if (err == null){
                if (result['result']['organizationpage'] === 'True'){
                    $('#organizationpage').addClass('active');
                } else {
                    $('#organizationpage').removeClass('active');
                }
            }
        })
    });
});
