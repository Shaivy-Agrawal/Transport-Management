function getTrainDetails() {
// fetch from server
fetch('url')
.then((resp) => {
    //response process

    var tt = document.getElementById("traintable");
    for (var i = 0; i < number_of_rows; i++) {
        var new_row = document.createElement("tr");

        var train_name = resp[i]['train_name'];
        var train_id = resp[i]['train_id'];
        new_row.innerHTML = `
        <td class='px-6 py-4 whitespace-no-wrap'> 
          <div class='flex items-center'> 
            <div class='flex-shrink-0 h-10 w-10'>
              <img class='h-10 w-10 rounded-full' src='https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-1.2.1&amp;ixid=eyJhcHBfaWQiOjEyMDd9&amp;auto=format&amp;fit=facearea&amp;facepad=4&amp;w=256&amp;h=256&amp;q=60' alt=''>
            </div>
            <div class='ml-4'>
              <div class='text-sm leading-5 font-medium text-gray-900'>
                Jane Cooper
              </div>
              <div class='text-sm leading-5 text-gray-500'>
                jane.cooper@example.com
              </div>
            </div>
          </div>
        </td>
        <td class='px-6 py-4 whitespace-no-wrap'>
          <div class='text-sm leading-5 text-gray-900'>` + train_name + `</div>` + `
          <div class='text-sm leading-5 text-gray-500'>Optimization</div>
        </td>
        <td class='px-6 py-4 whitespace-no-wrap'>
          <span class='px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800'>
            Active
          </span>
        </td>
        <td class='px-6 py-4 whitespace-no-wrap text-sm leading-5 text-gray-500'>
          Admin
        </td>
        <td class='px-6 py-4 whitespace-no-wrap text-right text-sm leading-5 font-medium'>
          <a href='#' class='text-indigo-600 hover:text-indigo-900'>Edit</a>
        </td>`;
    }
});
}