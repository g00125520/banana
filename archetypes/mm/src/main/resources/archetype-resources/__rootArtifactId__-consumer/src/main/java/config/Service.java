package ${package}.config;

/**
 * https://www.cnblogs.com/zhanqing/p/11076645.html
 */
public enum Service{

    USER("user-provider-h2");

    private String instance;

    private Service(String instance){
        this.instance = instance;
    }

    public String getInstance(){
        return this.instance;
    }

    public String toUrl(String location){
        StringBuffer sb = new StringBuffer("http://");
        sb.append(this.getInstance()).append("/").append(location);
        return sb.toString();
    }
}