
import paddle.nn as nn
import paddle
import paddle.nn.functional as F
# registry.LOSS.register('cross_entropy', nn.CrossEntropyLoss)


def dice_coeff(y_pred, y_true, smooth_value=1.0):
    inter = paddle.sum(y_pred * y_true)
    z = y_pred.sum() + y_true.sum() + smooth_value
    return (2 * inter + smooth_value) / z


def dice_loss_with_logits(y_pred: paddle.Tensor, y_true: paddle.Tensor, smooth_value=1.0, ignore_index=255):
    y_pred = y_pred.view(-1)
    y_true = y_true.view(-1)
    mask = y_true == ignore_index
    valid = ~mask
    y_true = y_true.masked_select(valid).float()
    y_pred = y_pred.masked_select(valid).float()
    return 1. - dice_coeff(y_pred.sigmoid(), y_true, smooth_value)


class DiceLoss(nn.Layer):
    def __init__(self,
                 smooth=1.0):
        super(DiceLoss, self).__init__()
        self.smooth = smooth

    def _dice_coeff(self, pred, target):
        """
        Args:
            pred: [N, 1] within [0, 1]
            target: [N, 1]
        Returns:
        """

        smooth = self.smooth
        inter = paddle.sum(pred * target)
        z = pred.sum() + target.sum() + smooth
        return (2 * inter + smooth) / z

    def forward(self, pred, target):
        return 1. - self._dice_coeff(pred, target)


class DiceWithLogitsLoss(nn.Layer):
    def __init__(self,
                 smooth=1.0):
        super(DiceWithLogitsLoss, self).__init__()
        self.smooth = smooth

    def _dice_coeff(self, pred, target):
        """
        Args:
            pred: [N, 1] within [0, 1]
            target: [N, 1]
        Returns:
        """

        smooth = self.smooth
        inter = paddle.sum(pred * target)

        z = pred.sum() + target.sum() + smooth
        return (2 * inter + smooth) / z

    def forward(self, pred, target):
        pred_score = F.sigmoid(pred)
        return 1. - self._dice_coeff(pred_score, target)
