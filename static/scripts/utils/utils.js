export const setDateTimeLocal = () => {
  const now = new Date();

  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, "0"); // Months are zero-indexed
  const day = String(now.getDate()).padStart(2, "0");
  const hours = String(now.getHours()).padStart(2, "0");
  const minutes = String(now.getMinutes()).padStart(2, "0");

  // Format: YYYY-MM-DDTHH:MM
	const formattedDateTime = `${year}-${month}-${day}T${hours}:${minutes}`;
	return formattedDateTime;
};
