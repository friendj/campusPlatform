$("#manager-center").load("html/manager-center/activity-management.html");
$(document).ready(function () {
    //活动管理
    $("#activity-management").click(
        function () {
            $("#manager-center").load("html/manager-center/activity-management.html");
        }
    );
    //招新管理
    $("#recruit-management").click(
        function () {
            $("#manager-center").load("html/manager-center/recruit-management.html");
        }
    );
    //本组织本社团信息
    $("#org-information").click(
        function () {
            $("#manager-center").load("html/manager-center/org-information.html");
        }
    );
    //发布活动
    $("#publish-activity").click(
        function () {
            $("#manager-center").load("html/manager-center/publish-activity.html");
        }
    );
});