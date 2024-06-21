template = """
<template>
  <view class="content">
    {{ template }}
  </view>
</template>
"""
script = """
<script>
{{ import }}

export default {
  components: {
    {{ components }}
  },
  data() {
    return {
      {{ data }}
    };
  },
  onLoad() {},
  methods: {},
};


</script>
"""