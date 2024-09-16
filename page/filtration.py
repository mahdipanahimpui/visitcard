


class Filtration:
    """
        important Note: Filteration class must be the first parrent class in child class
                        Otherwise, performance will be impaired
        important Note: the child class must inherit at least one of the subsequent classes that have get_queryset def
    """
    filtration_class = None
    pagination_class = None

    def check_filtration_class(self):
        if self.filtration_class is None:
            raise ValueError("Filtration_class is not defined.")
        
    def filter_queryset(self, queryset):
        try:
            return self.filtration_class().list(self.request, queryset)
        except Exception as e:
            raise RuntimeError("Filtration_class not provided in corrct way") from e

    def get_queryset(self):
        queryset = super().get_queryset()
        self.check_filtration_class()
        filtered_queryset = self.filter_queryset(queryset)
        
        return filtered_queryset
    
# --------------------------------------------------------------------------------------





######## Filtrations ########
# ------------------------------------------------------------------------------------
class BaseFilter:
    
    def handle_filter(self, request, queryset):
        return queryset

    def list(self, request, filtration_queryset):
        temp_queryset = filtration_queryset
        temp_queryset = self.handle_filter(request, temp_queryset)
        temp_queryset = OrderingQueryHandler(request).get_result(temp_queryset)
        return temp_queryset