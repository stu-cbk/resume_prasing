<template>

    <div class="introBox">

        <div class="titleBox">
            <p class="line"></p>
            <p class="title">
                <span>求职意向</span>
            </p>
        </div>

        <div class="introCon">
            <ul>
                <li>工作性质：全职</li>
                <li>期望职业：{{myiInfo.jobWant}}</li>
                <li>期望薪资：{{myiInfo.moneyWant}}</li>
            </ul>
        </div>

    </div>

</template>

<script>
export default {
    props: {
        myiInfo: {}
    },
};
</script>

<style lang="scss" scoped>

</style>