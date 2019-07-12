$("#student-center").load("html/student-center/follow-activity.html");
$(document).ready(function () {
    //已经关注活动
    $("#follow-activity").click(
        function () {
            $("#student-center").load("html/student-center/follow-activity.html");
        }
    );
    //已经报名活动
    $("#enroll").click(
        function () {
            $("#student-center").load("html/student-center/enroll.html");
        }
    );
    //已经关注社团活动
    $("#follow-org").click(
        function () {
            $("#student-center").load("html/student-center/follow-org.html");
        }
    );
    //活动证明
    $("#certification-download").click(
        function () {
            $("#student-center").load("html/student-center/certification-download.html");
        }
    );
    //用户信息
    $("#student-information").click(
        function () {
            $("#student-center").load("html/student-center/student-information.html");
        }
    );
});
