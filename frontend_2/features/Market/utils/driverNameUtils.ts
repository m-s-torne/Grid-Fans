/**
 * Extract last name from driver's full name
 */
export const getDriverLastName = (fullName: string): string => {
    const nameParts = fullName.trim().split(' ');
    return nameParts[nameParts.length - 1];
};
