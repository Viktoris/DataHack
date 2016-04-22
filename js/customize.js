/**
 * Created by Mário on 22.04.2016.
 */

Sk.onAfterImport = function(library) {
    switch(library) {
        case 'pygal':
            // make charts render instantly
            Highcharts.setOptions({
                plotOptions: {
                    series: {
                        animation: false
                    }
                }
            });
            break;
        case 'turtle':
            // make turtle draw instantly
            Sk.tg.defaults.animate = false;
            Sk.tg.Turtle.prototype.speed = function() {}
            Sk.tg.Turtle.prototype.delay = function() {}
            break;
    }
}