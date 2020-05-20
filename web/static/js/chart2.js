var auth = btoa('admin:admin');
function getPageTotalAndDataTotal() {
    var pageTotal = [];
    $.ajax({
        url:'http://172.26.129.233:5984/view_results(australia_tweets)/sa2_alcohol_senti_count',
        dataType:'json',
        async : false,
        xhrFields:{withCredentials:true},
        headers: {"Authorization": "Basic " + auth},
        crossDomain:true,
        success:function(data){
            pageTotal = data.rows;
        },
        error:function(data){
            console.log('request failed')
        }
    });
    return pageTotal;
}

function getSuburbInfo() {
    var DBdata = [];
    $.ajax({
        url:'http://172.26.129.233:5984/view_results(australia_tweets)/suburb_info',
        dataType:'json',
        async : false,
        xhrFields:{withCredentials:true},
        headers: {"Authorization": "Basic " + auth},
        crossDomain:true,
        success:function(data){
            DBdata = data;
        },
        error:function(data){
            console.log('request failed')
        }
    });
    return DBdata;
}

function getIncomeInfo() {
    var DBdata = new Array();
    $.ajax({
        url:'http://172.26.129.233:5984/aurin_result/sa2_map_twitter',
        dataType:'json',
        async : false,
        xhrFields:{withCredentials:true},
        headers: {"Authorization": "Basic " + auth},
        crossDomain:true,
        success:function(data){
            for (var item in data.features){
                var income_value = data.features[item]['properties']['median_total_household_income_weekly'];
                var educate_level = data.features[item]['properties']['degree_diploma_certificate_percent']
                DBdata[data.features[item]['properties']['SA2_MAIN16']] = [income_value,educate_level];
            }
            // DBdata = data.features;
            // console.log(DBdata)
        },
        error:function(data){
            console.log('request failed');
        }
    });
    return DBdata;
}

// var tweetCount=[];
var yXisdata=[];//=["Brunswick", "Brunswick East", "Thornbury", "Melbourne", "Southbank", "St Kilda", "Fitzroy", "Braeside", "Yarra Glen"];
var avgIncome=[];// = [1723, 1719, 1536, 964, 1855, 1616, 1708, 949, 1273];
var diploma_rate=[];// = [19.7183, 21.5613, 16.9811, 19.4444, 29.2683, 25.9112, 28.4314, 21.6867, 16.6667];
var suburb_info = getSuburbInfo();
var incomeInfo = getIncomeInfo();
var lii = getPageTotalAndDataTotal();

for (i=0; (i+2)<lii.length; i++) {
    if (lii[i].key[0] == lii[i + 2].key[0]){
        // var total = lii[i].value+lii[i+1].value+lii[i+2].value;
        for (var key in suburb_info){
            if (key == lii[i].key[0]){
                if (incomeInfo[key][1] != null){
                    yXisdata.push(suburb_info[key]);
                    avgIncome.push(incomeInfo[key][0]);
                    diploma_rate.push(incomeInfo[key][1])
                    break;
                }
            }
        } 
        i += 2;
    }
}
console.log(avgIncome)
console.log(diploma_rate)
var ectest = echarts.init(document.getElementById("sentiment2"));

option = {
    title: {
        text: 'Income versus Diploma rate of suburb',
        left: 'center'
    },
    dataZoom : [
        {
            type: 'slider',
            show: true,
            start: 0,
            end: 15,
            xAxisIndex: [0],
            minSpan: 5,
            maxSpan: 20,
            bottom: 'bottom',
            height: '20px'
        },
    ],
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'cross',
            crossStyle: {
                color: '#999'
            }
        }
    },
    legend: {
        data: ['income', 'diploma_rate'],
        top: '7%',
        padding:[0,5,5,0]
    },
    xAxis: [
        {
            type: 'category',
            data: yXisdata,
            axisPointer: {
                type: 'shadow'
            },
            axisLabel: {
                interval:0,
                rotate: -30
            }

        }
    ],
    yAxis: [
        {
            type: 'value',
            name: 'income',
            min: 0,
            max: 2700,
            interval: 300,
            axisLabel: {
                formatter: '{value} $'
            }
        },
        {
            type: 'value',
            name: 'diploma',
            min: 0,
            max: 45,
            interval: 5,
            axisLabel: {
                formatter: '{value} %'
            }
        }
    ],
    series: [
        {
            name: 'income',
            type: 'bar',
            data: avgIncome
        },
        {
            name: 'diploma_rate',
            type: 'bar',
            yAxisIndex: 1,
            data: diploma_rate
        }
    ]
};

ectest.setOption(option);