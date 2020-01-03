### opencv & tensorflow image data

---

Opencv: BGR

Tensorflow: RGB

**Normalized to -1~1**

```
cv::cvtColor(src, rgb, CV_BGR2RGB);

rgb.convertTo(rgb, CV_32FC3);

rgb /= 255.0f;

rgb -= cv::Scalar(0.5f, 0.5, 0.5);

rgb *= 2.0f;
```