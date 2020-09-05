function isFileImage(file) {
  const acceptedImageTypes = [
    "image/gif",
    "image/jpeg",
    "image/png",
    "image/webp",
  ];

  return file && acceptedImageTypes.includes(file["type"]);
}
