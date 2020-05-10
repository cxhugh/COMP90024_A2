         var ectest = echarts.init(document.getElementById("main-abcde"));
            var option = {
            xAxis: {
                 type: 'category',
                 data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            },
            yAxis: {
                 type: 'value'
            },
            series: [{
                    data: [820, 932, 901, 934, 1290, 1330, 1320],
                    type: 'line'
             }]
        };
            ectest.setOption(option);