# website-sizegrab
A Python script meant to be deployed on an AWS Lamba function that downloads the contents of a website and measures how much space it takes up on the disk.

Here are the things that still need to be handled:
- images/svgs declared in CSS

Here's an example URL to invoke the AWS Lambda function I've set up with this code:

`https://qksbtwafpnossajj2xxlhkp3qu0rsaof.lambda-url.us-west-2.on.aws/?website-to-test=https://www.julianlopez.net/`

To package this for Lambda run `pip install -r requirements.txt -t . && zip -r function.zip . && rm -r */`

Here's a [CodePen example](https://codepen.io/JLO64/pen/RwdrKaO) I have of this thing in action