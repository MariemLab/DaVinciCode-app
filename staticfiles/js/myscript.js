function deleteCategory(element) {
  // Get the category ID from the data attribute
  const categoryId = element.dataset.categoryId;

  // Confirm deletion
  if (confirm("Are you sure you want to delete this category?")) {
    // Send an AJAX request to the server to delete the category
    fetch(`/delete_category/${categoryId}/`, {
      method: "DELETE",
      headers: {
        "X-CSRFToken": csrfToken,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          // If the deletion is successful, remove the category from the UI
          element.parentElement.removeChild(element);
          alert("Category deleted successfully!");

          // You can add additional logic here, for example, redirecting to another page or updating other parts of the UI.
          // For example, redirect to the home page after deletion:
          window.location.href = "/";
        } else {
          alert("Failed to delete category. Please try again.");
        }
      })
      .catch((error) => {
        console.error("Error deleting category:", error);
        alert("An error occurred while deleting the category.");
      });
  }
}
