export function formatDate(dateObj: Date): string {
  const month = getMonthTwoDigits(dateObj.getMonth() + 1);
  const yr = dateObj.getFullYear();
  const date = dateObj.getDate();
  const hour = dateObj.getHours();
  const minutes = dateObj.getMinutes();
  const ms = dateObj.getMilliseconds();

  return `[${month}/${date}/${yr} ${hour}:${minutes}:${ms}]`;
}

function getMonthTwoDigits(month: number): string {
  return month < 10 ? `0${month.toString()}` : month.toString();
}
