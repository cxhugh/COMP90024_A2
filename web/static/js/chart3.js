// // var auth = btoa('admin:admin');
// // function getPageTotalAndDataTotal() {
// //     var pageTotal = [];
// //     $.ajax({
// //         url:'http://172.26.129.233:5984/view_results(australia_tweets)/sa2_alcohol_senti_count',
// //         dataType:'json',
// //         async : false,
// //         xhrFields:{withCredentials:true},
// //         headers: {"Authorization": "Basic " + auth},
// //         crossDomain:true,
// //         success:function(data){
// //             pageTotal = data.rows;
// //         },
// //         error:function(data){
// //             console.log('request failed')
// //         }
// //     });
// //     return pageTotal;
// // }

// // function getSuburbInfo() {
// //     var DBdata = [];
// //     $.ajax({
// //         url:'http://172.26.129.233:5984/view_results(australia_tweets)/suburb_info',
// //         dataType:'json',
// //         async : false,
// //         xhrFields:{withCredentials:true},
// //         headers: {"Authorization": "Basic " + auth},
// //         crossDomain:true,
// //         success:function(data){
// //             DBdata = data;
// //         },
// //         error:function(data){
// //             console.log('request failed')
// //         }
// //     });
// //     return DBdata;
// // }

// // function getIncomeInfo() {
// //     var DBdata = new Array();
// //     $.ajax({
// //         url:'http://172.26.129.233:5984/aurin_result/sa2_map_twitter',
// //         dataType:'json',
// //         async : false,
// //         xhrFields:{withCredentials:true},
// //         headers: {"Authorization": "Basic " + auth},
// //         crossDomain:true,
// //         success:function(data){
// //             for (var item in data.features){
// //                 var income_value = data.features[item]['properties']['median_total_household_income_weekly'];
// //                 var educate_level = data.features[item]['properties']['degree_diploma_certificate_percent']
// //                 DBdata[data.features[item]['properties']['SA2_MAIN16']] = [income_value,educate_level];
// //             }
// //             // DBdata = data.features;
// //             // console.log(DBdata)
// //         },
// //         error:function(data){
// //             console.log('request failed');
// //         }
// //     });
// //     return DBdata;
// // }

var yXisdata=["Brunswick", "Brunswick East", "Thornbury", "Melbourne", "Southbank", "St Kilda", "Fitzroy", "Braeside", "Yarra Glen"];
var avgIncome = [1723, 1719, 1536, 964, 1855, 1616, 1708, 949, 1273];
var diploma_rate = [19.7183, 21.5613, 16.9811, 19.4444, 29.2683, 25.9112, 28.4314, 21.6867, 16.6667];
// // var suburb_info = getSuburbInfo();
// // var incomeInfo = getIncomeInfo();
// // var lii = getPageTotalAndDataTotal();

// // for (i=0; (i+2)<lii.length; i++) {
// //     if (lii[i].key[0] == lii[i + 2].key[0]){
// //         var total = lii[i].value+lii[i+1].value+lii[i+2].value;
// //         if (total>60){
// //             tweetCount.push(total)
// //             for (var key in suburb_info){
// //                 if (key == lii[i].key[0]){
// //                     yXisdata.push(suburb_info[key]);
// //                     avgIncome.push(incomeInfo[key][0]);
// //                     diploma_rate.push(incomeInfo[key][1])
// //                     break;
// //                 }
// //             } 
// //         }
// //         i += 2;
// //     }
// // }
// // console.log(yXisdata);
// // // console.log(tweetCount);
// // console.log(avgIncome);
// // console.log(diploma_rate)

var ectest = echarts.init(document.getElementById("chart3"));

// option = {
//     title: {
//         text: 'Income versus Diploma rate of suburb',
//         left: 'center'
//     },
//     dataZoom : [
//         {
//             type: 'slider',
//             show: true,
//             start: 94,
//             end: 100,
//             handleSize: 8
//         },
//         {
//             type: 'inside',
//             start: 94,
//             end: 100
//         },
//         {
//             type: 'slider',
//             show: true,
//             yAxisIndex: 0,
//             filterMode: 'empty',
//             width: 12,
//             height: '70%',
//             handleSize: 8,
//             showDataShadow: false,
//             left: '93%'
//         }
//     ],
//     tooltip: {
//         trigger: 'axis',
//         axisPointer: {
//             type: 'cross',
//             crossStyle: {
//                 color: '#999'
//             }
//         }
//     },
//     legend: {
//         data: ['income', 'diploma_rate'],
//         y:'bottom',
//         padding:[0,5,5,0]
//     },
//     xAxis: [
//         {
//             type: 'category',
//             data: yXisdata,
//             axisPointer: {
//                 type: 'shadow'
//             },
//             axisLabel: {
//                 interval:0,
//                 rotate: -30
//             }

//         }
//     ],
//     yAxis: [
//         {
//             type: 'value',
//             name: 'income',
//             min: 800,
//             max: 2000,
//             interval: 300,
//             axisLabel: {
//                 formatter: '{value} $'
//             }
//         },
//         {
//             type: 'value',
//             name: 'diploma',
//             min: 10,
//             max: 30,
//             interval: 5,
//             axisLabel: {
//                 formatter: '{value} %'
//             }
//         }
//     ],
//     series: [
//         {
//             name: 'income',
//             type: 'bar',
//             data: avgIncome
//         },
//         {
//             name: 'diploma_rate',
//             type: 'bar',
//             yAxisIndex: 1,
//             data: diploma_rate
//         }
//     ]
// };


option = {
    title: {
    text: 'The alcohol tweets sentiment of suburb',
    left: 'center'
},
dataZoom : [
    {
        type: 'slider',
        show: true,
        start: 94,
        end: 100,
        handleSize: 8
    },
    {
        type: 'inside',
        start: 94,
        end: 100
    },
    {
        type: 'slider',
        show: true,
        yAxisIndex: 0,
        filterMode: 'empty',
        width: 12,
        height: '70%',
        handleSize: 8,
        showDataShadow: false,
        left: '93%'
    }
],
tooltip: {
trigger: 'axis',
axisPointer: {
    type: 'shadow'     //'line' | 'shadow'   　
},
formatter: '{b}<br />{a0}: {c0}%<br />{a1}: {c1}%<br />{a2}: {c2}%'
},
legend: {
x:'center',      //left bottom center
y:'bottom',     //left bottom center
padding:[0,5,5,0],
data: ['Neg', 'Neu', 'Pos']
},
grid: {
left: '3%',
right: '4%',
bottom: '3%',
containLabel: true
},
xAxis: {
type: 'value',
show: false
},
yAxis: {
type: 'category',
data: yXisdata
},
series: [
{
    name: 'Neg',
    type: 'bar',
    stack: 'percent',
    label: {
        show: true,
        position: 'right',
        formatter: '{c}%'
    },
    data: avgIncome
},
{
    name: 'Neu',
    type: 'bar',
    stack: 'percent',
    label: {
        show: true,
        position: 'insideRight',

            formatter: '{c}%'
    },
    data: diploma_rate
    },
]
};

ectest.setOption(option);