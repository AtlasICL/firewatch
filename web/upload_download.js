//TODO: add commenting
export async function uploadDownloadFile(file, apiEndpoint='https://j3w9dt7vyg.execute-api.eu-north-1.amazonaws.com/generate_url'){
    const presignResponse = await fetch(apiEndpoint, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({filename: file.name})
    });

    if(!presignResponse.ok){
        throw new Error('Failed to get S3 URL');
    }
    const{uploadUrl, downloadUrl, fileId, s3Key} = await presignResponse.json();

    const uploadResponse = await fetch(uploadUrl, {
        method: 'PUT',
        headers: { 'Content-Type': 'text/csv' },
        body: file
    });

    if(!uploadResponse.ok){
        throw new Error('S3 upload failed');
    }
    const downloadResponse = await fetch(downloadUrl);

    if (!downloadResponse.ok){
        throw new Error('S3 download failed');
    }
    const content = await downloadResponse.text();

    return{
        fileId,
        s3Key,
        content
    };
}

export default uploadDownloadFile;