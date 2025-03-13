<script>

    //import {myVarList} from '/Image_Query_by_Analysing_histogram/image-query/public/store'
    import Chart from "chart.js/auto";
    
    let imageInput;
    let my_image_file = ''
    let files;
    let imageInFrame = localStorage.getItem('imageInFrame');
    let imageSelectFlag = 1;
    let imageOutputFlag = 0;
    let imageOutput;
    let currentPage = 1;
    let totalPages;
    let pageInput = currentPage;
    let folderCounts = {};
    let chartInstance;
    let chartVisible = false;



    let algorithm = "Coweighed Semantic Convolutional Feature";
    let dataset = "Oxford5k";
    let isAlgoOpen = false;
    let isDataOpen = false;
    // let selectedOption = "Select an option";
    const algorithms = [
                        "Coweighed Semantic Convolutional Feature",
                        "Coweighed Semantic Convolutional Feature (38%)",
                        "Coweighed Semantic Convolutional Feature with GrayScaling (44%)",
                        "Coweighed Semantic Convolutional Feature (50%)",
                        "Coweighed Semantic Convolutional Feature (70%)",
                        // "Contrastive Weight Aggregation Histogram"
                       ];

    const datasets = ["Oxford5k", "Paris6k" ];


    

    /** @type {HTMLInputElement}*/


    // export const snapshot = {

    //     capture: () => {return imageInput.files},
    //     restore: (files) => imageInput.files = files
    // };

     

    // Update the store when needed
    // function updateVariableList(newImageValue) {
    //     myVarList.set(newImageValue);
    // }

    //$: countFolders();
    //$: if (Object.keys(folderCounts).length) drawPieChart();

    function countFolders() {
        folderCounts = {}; // Reset counts
        if (imageOutput.length === 0) return;

        imageOutput[currentPage - 1]?.forEach(imageChunk => {
            imageChunk.forEach(image => {
                let folderName = image[2].split("/")[0]; // Extract folder name
                folderCounts[folderName] = (folderCounts[folderName] || 0) + 1;
            });
        });
    }

    function generateChart() {
        countFolders(); // Update folder counts
        chartVisible = true; // Show chart

        // Ensure canvas exists
        setTimeout(() => { 
            if (!document.getElementById("folderPieChart")) return;

            const ctx = document.getElementById("folderPieChart").getContext("2d");

            // Destroy previous chart to prevent overlap issues
            if (chartInstance) chartInstance.destroy();

            chartInstance = new Chart(ctx, {
                type: "pie",
                data: {
                    labels: Object.keys(folderCounts),
                    datasets: [{
                        data: Object.values(folderCounts),
                        backgroundColor: ["red", "blue", "green", "orange", "purple"]
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,

                    plugins: {
                        legend: {
                            labels: {
                                font: {
                                    size: 16 ,// Change this value to increase font size
                                    weight : 'bold'
                                }
                            }
                        },
                        tooltip: {
                            bodyFont: {
                                size: 14 // Adjust tooltip font size
                            },
                            titleFont: {
                                size: 16 // Adjust tooltip title font size
                            }
                        }
                    }

                }
            });
        }, 10); // Small delay to ensure the chart container is updated
    }




    // Function to derive a relative path
    function getRelativePath(absolutePath, ds) {
        
        const imagePathParts = absolutePath.split('\\');
        let relativePath = imagePathParts.slice(imagePathParts.indexOf(ds)).join('/');
        relativePath = 'http://localhost:5000/' + relativePath
        //console.log(relativePath)

        return relativePath;
   }

   function chunkArray(arr, size, cluster) {
        const result = [];
        
        for (let i = 0; i < arr.length; i += cluster*size) {

            const subresult = []

            for(let j = 0; j < cluster*size; j += size){

                const chunk = arr.slice(i+j, i + j + size);

                if(chunk.length != 0){

                    subresult.push(chunk)

                }

            }

            result.push(subresult)

        }
        return result;
   }

    function getBase64(image) {
        imageSelectFlag = 0;
        const reader = new FileReader();

        my_image_file = image;
        reader.readAsDataURL(image);
        reader.onload = e => {
            imageSelectFlag = 1;
            imageInFrame = e.target.result;

            localStorage.setItem('imageInFrame',imageInFrame)

            //localStorage.setItem('image',reader.result)

            
            //myVarList.set(imageInFrame);

            // myVarList.subscribe(imageValue => {
            //     imageInFrame = imageValue;
            // }) 
        };
    };

    function handlePageInput(event) {
    let input = +event.target.value; // Convert input to number
    if (input > totalPages) {
      input = totalPages;
    } else if (input < 1) {
      input = 1;
    }

    currentPage = input;
    pageInput = currentPage;

    generateChart()

    chartVisible = true;

    // window.scrollTo({
    //   top: 0,
    //   behavior: 'smooth'  // This makes the scrolling smooth
    // });
        
    }

	const handleSearch = async () => {

        if(my_image_file == '' && imageInFrame != null) {
            var base64 = localStorage.getItem('imageInFrame')
            var base64parts = base64.split(",")
            var fileformat = base64parts[0].split(";")[0];
            var fileExt = fileformat.split("/")[1]
            var fileContent = base64parts[1];
            var bstr = atob(fileContent)
            var n = bstr.length
            var blob = new Uint8Array(n)

            while(n--){

                blob[n] = bstr.charCodeAt(n)
            }
            my_image_file = new File([blob],"a."+fileExt,{type : fileformat.split(":")[1]})

            console.log(fileformat)
            console.log(my_image_file)

        }

    
        const formData = new FormData();
        formData.append('image', my_image_file);
        formData.append('algorithm', algorithm);
        formData.append('dataset', dataset);

    
        console.log(my_image_file,algorithm)
    


        try {

        imageOutputFlag = 0
        const response = await fetch('./upload', {
            method: 'POST',
            body: formData,
        });

        const data = await response.json();
        console.log(data);

        imageOutput = chunkArray(data.image_list,3,8)

        totalPages = imageOutput.length

      //$page.imageOutput = imageOutput;

      //$page.page.router.push('/1');

    //   const relativePath = getRelativePath(imageOutput[0][0]);

        
       //console.log(localStorage.getItem('imageInFrame'))

        // console.log(imageOutput.length)

        currentPage = 1

        pageInput = 1


      imageOutputFlag = 1

      generateChart()

      chartVisible = true;


    } catch (error) {
      console.error('Error uploading image:', error);
    }
  };

  
    function toggleAlgoDropdown() {
        isAlgoOpen = !isAlgoOpen;
    }

    function selectAlgorithm(option) {

        
        algorithm = option;
        isAlgoOpen = false;

    }

    function toggleDataDropdown() {
        isDataOpen = !isDataOpen;
    }

    function selectDataset(option) {

        
        dataset = option;
        isDataOpen = false;

    }



    
</script>

<div>

<div class="container">
    
    {#if imageInFrame != null}
        <div id="frame">
            
            {#if imageSelectFlag === 1 }
                <img id="image_layer" src={imageInFrame} alt="uploaded_image"/>
            {/if}
            <img id="frame_layer" src="/frame.gif" alt="frame"/>
        </div>
        
    {:else}

        <img id="frame" src= "/frame.gif" alt="frame"/>
        
    {/if}
       
    <input class="hidden" id="file-to-upload" name= "image" type="file" accept=".png,.jpg,.gif" bind:files bind:this={imageInput} on on:change={() => getBase64(files[0])}/>
    <div class = "button-holder" >
        <button class="upload-btn" on:click= { () => imageInput.click() }>Upload</button>

        <button class="upload-btn" on:click= {handleSearch} >Search</button>

        <!-- <button class="upload-btn" on:click= {()=>{
            window.location.hash="#/1"
        }} >Go</button> -->

        <div class="dropdown-button" on:click={toggleAlgoDropdown} on:keypress={() => {}}>
            {algorithm}
        </div>
        
          {#if isAlgoOpen}
            <div class="dropdown-content">
              {#each algorithms as option}
                <div class="dropdown-item" on:click={() => selectAlgorithm(option)} on:keyup={() => {}}>
                  {option}
                </div>
              {/each}
            </div>
          {/if}

        <div class="dropdown-button" on:click={toggleDataDropdown} on:keypress={() => {}}>
            {dataset}
        </div>

        {#if isDataOpen}
            <div class="dropdown-content">
              {#each datasets as option}
                <div class="dropdown-item" on:click={() => selectDataset(option)} on:keyup={() => {}}>
                  {option}
                </div>
              {/each}
            </div>
          {/if}

    </div>

    <div class="button-holder">

    {#if imageOutputFlag === 1}

        <!-- <button class="upload-btn" on:click={generateChart}>Generate Pie Chart</button> -->

        <!-- Pie Chart (Only Visible When Button Clicked) -->

        {#if chartVisible}

        <div class="chart-container">
            <canvas id="folderPieChart"></canvas> 
        </div>

        
        {/if}

    {/if}

    </div>

    <!-- <div class="dropdown">
        
    </div> -->

    
</div>
    

<!-- <div> -->

    {#if imageOutputFlag === 1}

         
    {#each imageOutput[ currentPage - 1] as imageChunk, index(imageChunk)} 

        <div class="container">

            {#each imageChunk as image, index(image)}
                <div class = "image-container">
                    <a href={getRelativePath(image[0], dataset)}><img id="result_image_layer" src={getRelativePath(image[0], dataset)} alt={image[0]}/></a>
            
                    <p> Euclidian Distance : {image[1]} </p>
                    <p> File Name : {image[2]} </p>
                </div>
        
            {/each}

        </div>
        
    {/each}
    
    <div class="page-input">
        <label for="page-number">Go to Page: </label>
        <input
            id="page-number"
            type="number"
            min="1"
            max={totalPages}
            bind:value={pageInput}
            on:input={handlePageInput} />


        <span> / {totalPages}</span>
    </div>

    {/if} 

<!-- </div> -->

</div>   



<style>
    .container {
        display: flex;
        /*flex-direction: column;
        /*align-items: center;*/

        position: relative;
    }

    #frame {
        /*border-radius: 99999px;*/
        height: 512px;
        width: 512px;
        margin-bottom: 10px;
        /*overflow: hidden;*/
        position : relative;
    }

    #frame_layer {
        /*border-radius: 99999px;*/
        height: 512px;
        width: 512px;
        margin-bottom: 10px;
        /*overflow: hidden;*/
        position : absolute;
    }

    #image_layer {
        /*border-radius: 99999px;*/
        height: 390px;
        width: 390px;
        margin-bottom: 10px;
        margin-top: 75px;
        margin-left: 65px;
        /*overflow: hidden;*/
        position : absolute;
    }

    #result_image_layer {
        /*border-radius: 99999px;*/
        height: 390px;
        width: 390px;
        border: 2px black;
        margin-bottom: 50px;
        margin-top: 50px;
        margin-left: 65px;
        
        /* border-top: 5px ;
		border-left: 5px ;
		border-right: 5px ;
		border-bottom: 5px ; */
        /*overflow: hidden;*/
        
    }

    .hidden {
        display: none;
    }

    .button-holder {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 512px;
        justify-content: center;
        gap: 20px;
    
    }

    .image-container {
        /* display: flex; */
        /*flex-direction: column;*/
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;

        position: relative;
    }

    .upload-btn {
        width: 256px;
        height: 32px;
        background-color: black;
        font-family: sans-serif;
        color: white;
        font-weight: bold;
        border: none;
    }

    .upload-btn:hover {
        background-color: white;
        color: black;
        outline: black solid 2px;
    }

    .page-input {
        display: flex;
        justify-content: center; /* Center the input field and label */
        align-items: center;
        margin-top: 40px;
    }

    .page-input input {
        width: 50px;
        padding: 5px;
        text-align: center;
        margin-right: 10px; /* Space between input and total pages text */
        margin-left: 10px;
        margin-top: 10px;
    }

    .page-input span {
        margin-left: 10px; /* Space between input and total pages text */
    }

    /* .dropdown {
        position: relative;
        width: 
    } */

    .dropdown-button {
        width: 256px;
        height: 32px;
        padding-top: 10px;
        padding-bottom: 10px;
        cursor: pointer;
        background-color: #f1f1f1;
        border: 1px solid #ccc;
        border-radius: 4px;
        text-align: left;
    }

    /* .dropdown-button-data {
        width: 256px;
        height: 32px;
        padding-top: 10px;
        padding-bottom: 10px;
        cursor: pointer;
        background-color: #f1f1f1;
        border: 1px solid #ccc;
        border-radius: 4px;
        text-align: left;
    } */

    .dropdown-content {
        position: absolute;
        /* top: 100%;
        left: 0; */ 
        width: 256px;
        background-color: white;
        border: 1px solid #ccc;
        border-radius: 4px;
        box-shadow: 0px 8px 16px rgba(0, 0, 0, 0.2);
        max-height: 150px;
        overflow-y: auto;
        z-index: 10;
    }

    /* .dropdown-content-data {
        position: absolute;
        top: 100%;
        left: 0;  
        width: 256px;
        background-color: white;
        border: 1px solid #ccc;
        border-radius: 4px;
        box-shadow: 0px 8px 16px rgba(0, 0, 0, 0.2);
        max-height: 150px;
        overflow-y: auto;
        z-index: 10;
    } */

    .dropdown-item {
        padding: 10px;
        cursor: pointer;
    }

    /* .dropdown-item-data {
        padding: 10px;
        cursor: pointer;
    } */

    .dropdown-item:hover {
        background-color: #e1e1e1;
    }

    /* .dropdown-item-data:hover {
        background-color: #e1e1e1;
    } */

    
    .chart-container {
        width: 384px;
        height: 384px;
    }

</style>