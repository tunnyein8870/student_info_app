// Display Data at Frontend

// console.log(dict_data)
// const dataTableBody = document.getElementById("student-tbody");
// let sort_btn = document.createElement('btn');
// sort_btn.id = "sort";
// dataTableBody.append(sort_btn)

// dict_data.forEach((rowData)=>{
//     const row = document.createElement("tr");
//     for (const key in rowData) {
//       const cell = document.createElement("td");
//       cell.innerText = rowData[key];
//       row.appendChild(cell);
//     }
//     dataTableBody.appendChild(row);

//     document.getElementById('sort').onclick = ()=>{
//         document.getElementById('listOfCountries').innerHTML = "";
//         document.getElementById('countryList').innerHTML = "";
//         // document.getElementById('detail').innerHTML = "";
//         let sortGdp = rescl.sort(function(a,b){
//             return b.gdp - a.gdp;
//         });
//         for (let c in sortGdp){
//             let ctr = document.createElement('tr');
//             document.getElementById('countryList').append(ctr);
//             // ctable.innerHTML = sortGdp[c].area;
//             // console.log(sortGdp[c]);
//             ctr.innerHTML = `
//                 <td><img src='${sortGdp[c].flag}' style='width:60px; height:50px'></td>  
//                 <td>${sortGdp[c].name}</td>
//                 <th><b><i>GDP: </b></i></th>
//                 <td>${sortGdp[c].gdp.toLocaleString()}</td>
//             `;   
//         }
//     }
// });

// Another Sort Function
// let sortOrder = 1; // 1 for ascending, -1 for descending

// function sortTable(columnIndex) {
//   sortOrder = -sortOrder;
//   data.sort((a, b) => (a[Object.keys(a)[columnIndex]] > b[Object.keys(b)[columnIndex]]) ? sortOrder : -sortOrder);
  
//   const tableBody = document.getElementById("dataTableBody");
//   tableBody.innerHTML = "";

//   for (const row of data) {
//     const tr = document.createElement("tr");
//     tr.innerHTML = `
//       <td>${row.id}</td>
//       <td>${row.f_name}</td>
//       <td>${row.l_name}</td>
//       <!-- Add more cells here -->
//     `;
//     tableBody.appendChild(tr);
//   }
// }