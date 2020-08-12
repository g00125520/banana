package ${package}.annotation;

/**
 *使用注解标注不希望被componetscan扫描得类， 
 * 
 * @ComponentScan(excludeFilters = 
 *          {@ComponentScan.Filter(type=FilterType.ANNOTATION,value=ExcludeFromComponentScan.class)})
 * 
 */
public @interface ExcludeFromComponetScan {
}