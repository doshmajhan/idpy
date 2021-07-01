<script lang="ts">
  export let username: string;
  export let email: string;
</script>

<tr>
  <td class="px-6 py-4 whitespace-nowrap">
    <div class="text-sm font-medium text-gray-900">
      {username}
    </div>
    <div class="text-sm text-gray-500">
      {email}
    </div>
  </td>
  <td class="px-6 py-4 whitespace-nowrap">
    <div class="text-sm text-gray-900">company:roles</div>
    <div class="text-sm text-gray-500">team:roles</div>
  </td>
  <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
    <a href="#" class="text-indigo-600 hover:text-indigo-900">Edit</a>
  </td>
</tr>